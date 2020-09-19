var store = [{
        "title": "openSystem()",
        "excerpt":"Description openSystem() is a function used to load the simulation files to be analysed. The function can load either single frames or whole trajectory. Only one type of molecule will be extracted from the files, since Machine Learning models can only be generated on one molecule type at the time....","categories": ["api"],
        "tags": ["system"],
        "url": "http://localhost:4000/mllpa/documentation/api/common/1-opensystem/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "generateModel()",
        "excerpt":"Description generateModel() is a function used to train Machine Learning models to predict the phases of molecules based on the input systems. The models will be saved in a file unless told otherwise, and will also output the models in a variable that can be used directly. Argument, keywords and...","categories": ["api"],
        "tags": ["training"],
        "url": "http://localhost:4000/mllpa/documentation/api/common/2-generatemodel/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Load from simulation files",
        "excerpt":"In order to analyse a simulation with ML-LPA, the simulation files should first be loaded into ML-LPA. We describe in this tutorial how to load the files. Load the files Single frame This is done using the openSystem() function. To load a single frame (no trajectory), one can use directly...","categories": ["tutorial"],
        "tags": ["file access","system"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/loading-files/1-simulation-files/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Load from position array",
        "excerpt":"In certain cases, it could be desirable to load directly the positions and configurations not from simulation files but from position arrays, as supported by NumPy. We describe in this tutorial how to proceed. Please be aware that loading a system from a position array can be a complicated and...","categories": ["tutorial"],
        "tags": ["file access","system"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/loading-files/2-positions/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "The .lpm model file",
        "excerpt":"ML-LPA uses its own file type to store the trained Machine Learning models: the .lpm files (Lipid Phase Model). This tutorial explore thoroughly these files. The .lpm file format The .lpm are neither text nor binary files: they are in fact .zip compressed files with a custom extension. Inside the...","categories": ["tutorial"],
        "tags": ["machine learning","system","output"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/outputs/1-model-file/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Save the System class",
        "excerpt":"Once the phases of the system have been predicted by ML-LPA - or assigned manually - it can be essential to store and save the results in a file on your computer. This tutorial will explain how it can be easily done. Pick the file format When an instance of...","categories": ["tutorial"],
        "tags": ["file access","system","output"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/outputs/2-save-system/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Save the Tessellation class",
        "excerpt":"Similarly to the instances of the System class, the instances of the Tessellation class can be stored in a file, and saved in multiple formats. This tutorial develops how this should be done.   (TO BE COMPLETED)   Check the API   The following elements have been used in this tutorial:      saveVoro  ","categories": ["tutorial"],
        "tags": ["file access","system","output"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/outputs/3-save-voronoi/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Machine Learning algorithms training",
        "excerpt":"Once the simulation files have been extracted and their information stored in instances of the System class, ML-LPA is ready to be trained to identify the lipid phases. Requirements for the systems ML-LPA can be trained to predict multiple phases at the same time (# phases &gt;= 2). For each...","categories": ["tutorial"],
        "tags": ["machine learning","system","training"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/phase-prediction/1-training/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Optimisation of the neighbour rank",
        "excerpt":"The intra-molecular atom distances are a critical feature of the molecules used by ML-LPA to analyse and then predict the lipid phases. However, this feature is based on the given neighbour rank, for which the optimal value has to be determined by the user. This tutorial demonstrates how ML-LPA can...","categories": ["tutorial"],
        "tags": ["machine learning","system","training"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/phase-prediction/2-rank-optimisation/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Lipid phase prediction",
        "excerpt":"Once the models have been generated through ML-LPA, they can be used, either from the .lpm file or from the variable, to predict the phase of a simulation with an unknown composition. This tutorial shows how to proceed. Predict phases From an *.lpm file To predict the lipid phases in...","categories": ["tutorial"],
        "tags": ["machine learning","system","prediction"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/phase-prediction/3-ml-prediction/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Setting phases manually",
        "excerpt":"Depending on the situation, some lipids - or other membrane molecules - might not undergo a phase transition during the simulations. For instance, the dioleoyl-glycerophosphocholine (DOPC) has a transition temperature of -17C, so it more than likely that it will remain in the fluid phase for all simulations run in...","categories": ["tutorial"],
        "tags": ["machine learning","system","prediction"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/phase-prediction/4-set-phases/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Quick & Dirty tutorial",
        "excerpt":"While it is recommended to read the whole tutorials before getting started with ML-LPA, we present on this page a quick and dirty example on how ML-LPA can be used to analyse a set of simulation files. In the following example, we will use two simulations (one at low temperature,...","categories": ["tutorial"],
        "tags": [],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/quick-and-dirty/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Attributes of the System class",
        "excerpt":"In a standard quick and dirty use of ML-LPA, using or just accessing the attributes of an instance of the System class does not bear too much interest. However, it is good to know what can be found inside the class if needed. We describe in this tutorial some of...","categories": ["tutorial"],
        "tags": ["system"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/system-class/1-description/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Methods of the System class",
        "excerpt":"Similarly, to the attributes, the methods of an instance of the System class does not bear too much interest in a standard quick and dirty use of ML-LPA. We describe in this tutorial some of the most useful methods of the class. If you are only interested in getting ML-LPA...","categories": ["tutorial"],
        "tags": ["system"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/system-class/2-methods/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Voronoi tessellations",
        "excerpt":"Besides the phase prediction, the other key feature of ML-LPA is its capacity to analyse the local environment of membrane molecules. This is done by performing Voronoi tessellations in order to list the direct neihbors of each molecule. Defining the geometry Ghost lipids Doing a 2-Dimension Voronoi tessellations of a...","categories": ["tutorial"],
        "tags": ["voronoi","tessellations","neighbors"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/tessellations/1-voronoi/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Map the environment",
        "excerpt":"Once the tessellation has been processed on the system and the instance of the Tessellation class generated, ML-LPA is ready to map the local environment of the lipids. Local environment Inside a membrane, a lipid A is always surrounded by N lipids Bi. Each of these Bi belongs to a...","categories": ["tutorial"],
        "tags": ["voronoi","tessellations","neighbors"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/tessellations/2-local-environment/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },{
        "title": "Analysis without phases",
        "excerpt":"While ML-LPA has been ultimately designed and developed to analyse the lipid phases, the tools used to analyse the local environment can be used investigate other types of environment than the phases. Setting In this tutorial, we will see how to do that by analysing a mixture of DLPC and...","categories": ["tutorial"],
        "tags": ["voronoi","tessellations","neighbors"],
        "url": "http://localhost:4000/mllpa/documentation/tutorials/tessellations/3-no-phases/",
        "teaser": "http://localhost:4000/mllpa/assets/images/logo.png"
      },]
