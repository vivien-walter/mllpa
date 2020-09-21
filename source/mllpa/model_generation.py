import numpy as np
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from tqdm import tqdm

from mllpa.input_output import openModelFile
from mllpa.interface_communication import _is_int, _is_float, _is_dict, _is_file_is, _is_list_of, _error_training_size, _error_input_type, _error_out_of_range

##-\-\-\-\-\-\-\-\-\
## SYSTEM PREPARATION
##-/-/-/-/-/-/-/-/-/

# -----------------------------------------------------------------
# Format the configurations for input in the machine learning model
def _format_input(coordinates, distances):

    # Reshape the coordinate array
    coordinates = np.reshape(coordinates, (coordinates.shape[0], coordinates.shape[1], coordinates.shape[2]*2))
    coordinates = np.concatenate(coordinates)

    # Reshape the distance array
    distances = np.concatenate(distances)

    return coordinates, distances

# -------------------------------------------
# Format multiple systems into a training set
def _format_training_set(systems, phases=['gel', 'fluid']):

    # Check the phases format
    if not _is_list_of(phases, type='string', check_array=True, recursive=False):
        _error_input_type('Phases', 'list of '+str(str))

    # Process all the systems
    all_coordinates = []
    all_distances = []
    all_states = []
    for i, system in enumerate(systems):

        # Format the input
        current_coordinates, current_distances = _format_input(system.coordinates, system.distances)

        current_states = np.array( [phases[i]] * current_coordinates.shape[0] )

        # Add the positions to the array
        all_coordinates.append( current_coordinates )
        all_distances.append( current_distances )
        all_states.append( current_states )

    # Merge all arrays
    all_coordinates = np.concatenate(all_coordinates)
    all_distances = np.concatenate(all_distances)
    all_states = np.concatenate(all_states)

    return all_coordinates, all_distances, all_states

# ------------------------
# Load the model from file
def load_models_file(path_file):

    # Load the training sets from the file
    coordinates, distances, states, metadata_content = openModelFile(path_file)
    training_infos = metadata_content['training']

    # Train the models on the loaded sets
    validationSize, seed, nSplits = training_infos['validation_size'], training_infos['seed'], training_infos['n_splits']
    models, _scores, _errors = trainModel(coordinates, distances, states, validationSize=validationSize, seed=seed, nSplits = nSplits)

    return models, training_infos

# ---------------------------------------
# Get the models from the provided source
def _get_models_from_source(models):

    # Get the models from a file
    if _is_file_is(models, extensions=['.lpm'], exist=True, no_extension=False):
        trained_models, training_infos = load_models_file(models)

        return trained_models, training_infos

    # Get the models from a dictionary
    elif _is_dict(models):
        return models, None

    else:
        _error_input_type("Models","model file or model dictionary")

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## MACHINE LEARNING ALGORITHMS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# ----------------------------------
# Evaluate the score of a prediction
def _get_score(prediction, label, score_dictionnary = None):

    # Initialise the dictionnary
    if score_dictionnary is None:
        score_dictionnary = {}

    # Get the total number
    prediction_number = prediction.shape[0]

    # Split the array between correct and false predictions
    correct_guess = prediction[prediction == label]
    wrong_guess = prediction[prediction != label]

    # Save the corresponding score
    score_dictionnary['total'] = correct_guess.shape[0] / prediction_number

    # Get the phase specific predictions
    for phase in np.unique(correct_guess):
        correct_phase = correct_guess[correct_guess == phase]
        wrong_phase = wrong_guess[wrong_guess == phase]

        score_dictionnary[phase] = correct_phase.shape[0] / (correct_phase.shape[0] + wrong_phase.shape[0])

    return score_dictionnary

# ------------------------------------------------
# Get the detailed score of a given list of models
def _make_detailed_score(models, verification_coordinates, verification_distances, verification_labels):

    # Predict the phases
    prediction_array = _prediction_array(verification_coordinates, verification_distances, models)

    # Initialise the score dictionnary
    scores = {}

    # Get the score of each model prediction
    for i, model_name in enumerate(['SVM_Coordinates','KNN_Coordinates','SVM_Distances','NB_Distances']):
        scores[model_name] = _get_score(prediction_array[:,i], verification_labels)

    # Get the score of the decision tree
    final_prediction = _final_decision(prediction_array, models)
    scores['final_score'] = _get_score(final_prediction, verification_labels)

    return scores

# -----------------------------------------
# Merge all scores to calculate the average
def _merge_scores(score_array):

    # Get the template dictionnary for the generation
    reference_dict = score_array[0]

    # Collect all the scores
    score_means = {}
    score_errors = {}

    # Process all the scores
    for model in reference_dict.keys():

        # Initialise the dictionnary
        score_means[model] = {}
        score_errors[model] = {}

        # Process all the phases
        for test in reference_dict[model].keys():

            # Gather all the scores
            current_scores = [x[model][test] for x in score_array]

            # Save the average and error
            score_means[model][test] = np.mean(current_scores)
            score_errors[model][test] = np.std(current_scores, ddof=1)

    return score_means, score_errors

#-------------------------------------------
# Generate the ML model for phase prediction
def trainModel(coordinates, distances, states, validationSize=0.20, seed=7, nSplits = 10):

    # Check the inputs
    if not _is_float(validationSize, strict=True):
        _error_input_type('First frame',str(float))
    elif validationSize < 0.01 or validationSize >= 0.33:
        _error_out_of_range(validationSize, 'Validation size', 0.01, 0.33)

    if not _is_int(seed):
        _error_input_type('Seed',str(int))

    if not _is_int(nSplits):
        _error_input_type('Number repetitions',str(int))
    elif nSplits <= 0:
        _error_out_of_range(nSplits, 'Number repetitions', 1, "inf")

    # Check the validation subset size
    _error_training_size(coordinates.shape[0] / np.unique(states).shape[0], validationSize)

    # Make an ID array
    systems_IDs = np.arange(states.shape[0])

    # Prepare the scoring and model selections
    best_total_score = 0
    best_models = {}

    all_scores = []

    # Do several trainings and verifications to get an average score
    for i in tqdm(range(nSplits), desc="Training models..."):

        # Split the ID and label into training and verification subsets
        ids_training_1, remaining_ids, states_training_1, remaining_states = model_selection.train_test_split(systems_IDs, states, test_size=2*validationSize, random_state=seed+i)
        ids_training_2, ids_verification, states_training_2, states_verification = model_selection.train_test_split(remaining_ids, remaining_states, test_size=0.5, random_state=seed+i)

        # Split all the dataset
        coordinates_training_1 = coordinates[ids_training_1]
        coordinates_training_2 = coordinates[ids_training_2]
        coordinates_verification = coordinates[ids_verification]

        distances_training_1 = distances[ids_training_1]
        distances_training_2 = distances[ids_training_2]
        distances_verification = distances[ids_verification]

        # Train each model
        svm_coordinates_model = SVC(gamma='scale').fit(coordinates_training_1, states_training_1) # SVM on coordinates
        knn_model = KNeighborsClassifier().fit(coordinates_training_1, states_training_1) # KNN on coordinates
        svm_distances_model = SVC(gamma='scale').fit(distances_training_1, states_training_1) # SVM on distances
        nb_model = GaussianNB().fit(distances_training_1, states_training_1) # NB on coordinates

        # Generate the dictionary with the models
        models = {
        'SVM_Coordinates': svm_coordinates_model,
        'KNN_Coordinates': knn_model,
        'SVM_Distances': svm_distances_model,
        'NB_Distances': nb_model
        }

        # Use the models to make the prediction on the second training set
        final_training = _prediction_array(coordinates_training_2, distances_training_2, models)

        # Convert the string array into a binary one
        final_training_binary = np.zeros(final_training.shape)
        for i, state_name in enumerate( np.sort(np.unique(states)) ):
            final_training_binary[final_training == state_name] = i

        # Train the classification tree
        final_model = DecisionTreeClassifier().fit(final_training_binary, states_training_2)

        # Add the model to the dictionnaries
        models['ClassificationTree'] = final_model

        # Do all the scores
        model_scores = _make_detailed_score(models, coordinates_verification, distances_verification, states_verification)

        # Save the scores for general measurement
        all_scores.append(model_scores)

        # Save the models if needed
        if model_scores['final_score']['total'] > best_total_score:
            best_total_score = model_scores['final_score']['total']
            best_models = models

    # Merge the scores to generate the average score
    training_scores, training_errors = _merge_scores(all_scores)

    return best_models, training_scores, training_errors

#------------------------------------------------------------------------
# Combine the predictions of all models to determine the final prediction
def _final_decision(predictions, models):

    # Get the trained model
    classification_tree = models['ClassificationTree']

    # Convert the string array into a binary one
    final_training_binary = np.zeros(predictions.shape)
    for i, state_name in enumerate( np.sort(np.unique(predictions)) ):
        final_training_binary[predictions == state_name] = i

    # Read the prediction
    prediction = classification_tree.predict(final_training_binary)

    return prediction

# -----------------------------
# Generate the prediction array
def _prediction_array(coordinates_space, distance_space, models):

    # Get the models
    svm_coordinates_model = models['SVM_Coordinates']
    knn_model = models['KNN_Coordinates']
    svm_distances_model = models['SVM_Distances']
    nb_model = models['NB_Distances']

    # Predict the phase with each model
    svm_c_prediction = svm_coordinates_model.predict(coordinates_space)
    knn_prediction = knn_model.predict(coordinates_space)
    svm_d_prediction = svm_distances_model.predict(distance_space)
    nb_prediction = nb_model.predict(distance_space)

    # Generate the prediction array
    prediction_array = np.stack((svm_c_prediction, knn_prediction, svm_d_prediction, nb_prediction),axis=1)

    return prediction_array

# ----------------------------------
# Predict the state of the molecules
def makePredictions(coordinates, distances, models):

    # Get the predictions array from the models
    individual_predictions = _prediction_array(coordinates, distances, models)

    # Make the final decision
    final_predictions = _final_decision(individual_predictions, models)

    return final_predictions
