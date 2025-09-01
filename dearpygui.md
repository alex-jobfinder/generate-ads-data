# Think of 5-10 dearpygui GUI applications for my app. Here are some ideas for reference. 

Potential Dear PyGui Applications

    Data Generation Dashboard
    Configure datasets (size, time range, profiles), run generation, and watch progress logs in real time.

    Campaign Profile Builder
    Interactive editor for YAML/JSON campaign profiles with validation and preview of resulting objects.

    Workflow Visualizer
    Graphically inspect how processors, validators, and generators connect; ideal for explaining or debugging workflows.

    Performance Metrics Explorer
    Plot CTR, viewability, and other generated metrics over time, with filtering by campaign, flight, or platform.

    Schema & ERD Viewer
    Browse SQLAlchemy/SQLite schema visually, drill into tables, and inspect relationships or constraints.

    DBT Model Runner
    Select models/seeds/tests from the dbt project, execute them, and show run logs and output tables.

    Data Validation Monitor
    Display pending validations, show constraint failures or Pydantic errors, and suggest fixes.

    Export & Integration Manager
    Pick datasets, format (CSV/Parquet/SQLite), and destination; track job status and summarize results.

    Command-line Wrapper
    GUI front-end for your CLI (init-db, generate, etc.), with parameter fields and saved presets.

    Ad Creative Previewer
    Load creative metadata, preview media, and review associated performance metrics side-by-side.

# More ideas: 

Dear PyGui App Ideas

Campaign Explorer: Browse advertisers, campaigns, line items, creatives with master-detail panes; inline edit status/CPM; quick filters for objective/status. (Tables, tree views, search bar)

Performance Dashboard: Time-series of impressions/clicks/CTR/CPM with date pickers and campaign multi-select; compare vs. target lines. (Plot lines/bars, range slider)

CPM Optimizer: Input budget/objective; see suggested CPM and estimated reach; sensitivity curves and sliders to tune assumptions. (Sliders, live plot, value boxes)

ROI Forecaster: Select campaign, days, and seasonal flag; show forecast table/graph and scenario bands (conservative/realistic/optimistic). (Tabs, area chart, datagrid)

A/B Test Designer: Configure variants (copy, format, duration), traffic split, and test duration; preview outcomes and export test plan. (Forms, dual panels, pie chart)

Creative QA Viewer: Gallery of creatives per line item with metadata (duration, file size, mime); highlight QA status and flags; quick approve/reject. (Image grid, tag/status chips)

Audience Targeting Sandbox: Build targeting rules (geo/device/format) via node/graph editor; simulate reach and CPM impacts. (Node editor, badges, live KPI panel)

Seasonal Trends Heatmap: Heatmap of performance by weekday/hour; drill into periods; annotate holidays/back-to-school effects. (Heatmap, tooltips, date controls)

Schema & ERD Browser: Inspect tables/columns/indexes and row counts; visualize relationships; copy sample queries. (Collapsing headers, graph nodes/edges, code blocks)

Data Generator Wizard: Guided flow to create advertiser/campaign and optionally generate performance; review JSON before persisting. (Wizard steps, JSON viewer, progress bar)

## https://github.com/hoffstadt/DearPyGui/wiki/Dear-PyGui-Showcase

Dear PyGui Showcase
Raccoon edited this page on Mar 8, 2024 · 116 revisions

The following apps have been developed with Dear PyGui by various developers and show the versatility of Dear PyGui. Dear PyGui is a fast, easy to use and powerful Python cross-platform GUI library (Windows, Linux and MacOS) available under a permissive MIT license. With Dear PyGui, one can build traditional desktop apps, yet one can create more graphically dynamic applications as well.
Flux

Flux is a beautiful dynamic flowfield visualization with particle simulation. It demonstrates the movement of particles within a vector field, offering an engaging visualization of the underlying noisemaps.

Flux flowfield
DearEIS: Electrochemical Impedance Spectroscopy

DearEIS is a Python package that includes both a program with a graphical user interface (GUI) and an application programming interface (API) for working with impedance spectra. The target audience is researchers who use electrochemical impedance spectroscopy (EIS) though the program can also be used in educational settings. DearEIS has a project-based workflow and multiple projects can be open at the same time. Each project has a user-definable label and a section for keeping notes. Multiple projects can also be merged to form a single project. You can read more about DearEIS in this article.

DearEIS example 1

Data sets and their corresponding results (Kramers-Kronig tests and equivalent circuit fits) are visualized using simple Nyquist plots, Bode plots, and residual plots. More complex plots containing multiple data sets, Kramers-Kronig test results, equivalent circuit fitting results, and/or simulation results can also be created. More information is available on the DearEIS project page and in the Github repository.

DearEIS example 2
FlowTutor: A graphical programming environment using flowcharts

FlowTutor is an application to help teach programming to engineering students. It illustrates the structure of a Python application, inclusing loops, if-else clauses and function calls visually while the Python application runs. FlowTutor shows the values of the variables, a log of the output and allows for setting of breakpoints.

FlowTutor
Image processing node editor

Image processing node editor is an application that performs image processing with the node editor (see video). It is used for processing verification and comparison. The node editor allows the user to select a video source to process nodes. Process nodes can apply processing in the form of cropping, blurring, generating a colour map or RGB graph, changing brightness or contrast or other filter types. The processed node can then be used as input for multiple deep learning nodes, such as classification, face detection, object detection or others. The results of the various nodes can be combined into multiple output nodes, for example a video writer to export the results to a video file. All of the processing, plotting and output is executed in real-time. The source code is available in the Github repository.

Image processing node editor
P1125: Profiling current of battery powered devices

The P1125 is hardware device for profiling current of battery powered devices with deep sleep modes and high current active states, made by Sistemi Corp. This is useful for developing and testing IoT devices. The P1125 is designed to be used by the designer at their desk to gain insight into the target current usage profile. The P1125 makes measuring current as easy as measuring voltage. The hardware is used in combination with a custom application written in Python with a user interface made with Dear PyGui. The application includes many controls and plotting options for interactively gaining insight into a dataset containing over a million data points. The software is proprietary, which is in accordance with Dear PyGui's MIT license. The MIT license allows you to keep your app proprietary, to sell it commercially or make it open source applications without any obligations. A more extensive demonstration of this app can been viewed on YouTube.

P1125
Wordle clone

Simple Python clone of the web-based game Wordle, originally created by Josh Wardle.

Wordle
KrxImpExp: 3D asset import/export Blender add-on

KrxImpExp is an open-source 3D asset import and export Blender add-on for modding Gothic 1 and 2 games. It is a hard fork for modern 2.8+ Blender and has been written with use of Dear PyGui as the original wxWidgets framework UI project was unmaintainable. The team decided to use Dear PyGui due to it's language (Blender uses Python for add-ons), size, simplicity and extensibility to further improve the user experience. The Dear PyGui UI offers seamless integration with the Blender user interface. The source code is available in the GitLab repository.

KrxImpExp
contExt: Image processor

contExt performs treatment and contour extraction from an image, and the generation of sparse or adaptive meshes intended for the application of numerical methods, especially finite differences.

contExt: Image processor
TRESMENT - Team Resource Management

TRESMENT is a proprietary Team Resource Management tool built with Python and Dear PyGui. The app combines many features of Dear PyGui to create an intuitive and user friendly interface. The interface forges tables, listboxes, checkboxes, drop-down menus, tree nodes and modal popup menus into a singular, smooth workflow. In addition, the program leverages Dear PyGui's flexible theming system to provide the users with the option to choose between a light or dark mode.

TRESMENT showcase
Asset Builder

Asset Builder is a tool for choosing, recolorizing, and stacking images together of the same type, typically used for creating 2D games. The source code is available under an MIT license and can be downloaded from the project's Github repository. A stand-alone executable version, built with Nuitka, is available for Linux and Windows.

Asset Builder
YaChiPy

YaChiPy is a Chip-8 Emulator with debug features. Step back in time and experience the charm of retro gaming. This app emulates the Chip-8 games exactly how they were, including the typical occasional blinking of the graphics. This emulator comes equipped with advanced debug features to enhance your gaming and programming experience. Pause the emulator at any moment to inspect the state of the virtual machine. Take control of time with the ability to speed up or slow down the CPU clock. The memory contents, register values, and timer values are displayed in real-time. You can load your favorite ROMs and customize settings.

YaChiPy
Froyo: Utility for downloading works from Archive Of Our Own

Froyo is a small graphical application for downloading works from Archive Of Our Own (AO3). It supports batch downloading of works to supported formats (AZW3, EPUB, HTML, MOBI, PDF). The app is small, fast and functional, a perfect fit for Dear PyGui. Not every app has to be complex. Sometimes a tool just needs to get the job done. The source code is available in the Github repository.

Froyo
Raccoon Music Player

Raccoon Music Player is a pocket-sized music player that shows raccoons dancing around a campfire while songs are playing. It's a proof-of-concept app that was made with Python using the excellent Dear PyGui and PyMiniAudio libraries and has no other dependencies. Raccoon Music Player can play MP3, WAV and FLAC music files. A longer and higher quality video as well as the source code can be found in the Github repository.

Raccoon Music Player
RaViewer: parsing and displaying binary data acquired straight from camera

RaViewer is an open-source utility dedicated to parsing and displaying binary data acquired straight from camera. After opening a binary image, you can specify the color format, the image size and append or remove n bytes from the beginning of the image series. The binary image will be processed and shown based on these values. You can control which color channels are displayed and zoom in and out. For detailed information, you can view the hexadecimal pixel values in table format. The resulting image can be exported entirely or just a selected part to more complex formats (JPEG, PNG) or raw data. The source code is available in the project's GitHub repository.

RaViewer
DearBagPlayer

DearBagPlayer is a flexible rosbag player based on Dear PyGui in Python. ROS stands for Robot Operating System. A bag is a file format in ROS for storing ROS message data. Bags, so named because of their .bag extension, have an important role in ROS. This tool allows the user to load various data file and visualize the distinct, but related data in four different graphs simultaneously. The app allows for dragging and dropping of files on the the four graph areas and dynamically zooming in on parts of graphs. The interactive and dynamic graphs are a feature of Dear PyGui. The source code is available in the Github repository.

!DearBagPlayer
VLM Streamer

VLM Streamer is a Vision and Machine Learning data streamer for SideFX Houdini. This program was made as a utility tool for Sidefx Houdini, but nothing is holding you back from using it as a generic data server to feed your own udp client that decodes the data. A more extended demonstration of shown in this video.

VLM Streamer
Pomodoro Timer

Pomodoro timer is a GUI utility for setting a Pomodoro timer for task, short and long break time. The source code is available in the Github repository.

POMODORO
Heron: A Hybrid Approach to Data Pipelines in Python

Heron is a Python only graphical editor designed to initiate, connect and orchestrate multiple processes, potentially running on multiple computers. Each process is graphically represented as a node with inputs and outputs. Connecting an output of one process to the input of another will result in the data generated by the output process to be passed to the input one, subsequently triggering the input processes functionality. The philosophy behind this app has been described in this article. All visual items shown in the screenshot below, including the node editor, are created with Dear PyGui. The source code is available in the Github repository.

Heron
CAN Explorer: Bus visualization tool

can-explorer is a CAN bus visualization tool designed to aid in reverse engineering. By continuously plotting all payloads for each CAN id, spotting trends that correspond to a specific action can become significantly easier to identify. can-explorer demonstrates the ability of creating and updating multiple real-time graphs with Dear PyGui. The application provides an example of how to combine threading and Dear PyGui.

CAN Explorer
YouTube captions to e-book

The YouTube captions to e-book app takes any YouTube video URL and downloads the video cover and captions in any available language and turns it into an e-book. Such e-books can provide a valuable resource for learning and studying a language. The source code is available in the project's GitHub repository.

YouTube captions to e-book
ELPath: An algorithm visualizer

ELPath is lovingly built using DearPyGui as a basis for its GUI and plotting functions. This is aimed at providing understandable visualizations of common sorting and pathfinding algorithms. Visualizations include Quick Sort, Merge Sort, Bubble Sort, Insertion Sort, Selection Sort, Cocktail Sort, Breadth and Depth-First Search, Dijkstra's Algorithm, and A* Search.

ELPath
TAP ADQL Sandbox

TAP ADQL Sandbox is an application for executing ADQL queries via TAP interface of various data sources, such as astronomical databases. TAP stands for Table Access Protocol, which is a way to query data from a database. ADQL stands for Astronomical Data Query Language and it is very similar to SQL, just with extended functionality for performing various operations on the data, such as geometrical functions. Essentially, it's a GUI for PyVO. The idea is that one can quickly run and test ADQL queries using this application and then add the final query to an application or notebook. This would be of interest to planetary scientists and astronomers, as most astronomical databases expose their data via TAP interface. The source code is available in the Github repository.

TAP ADQL Sandbox
Tetris

Tetris is a remake of the original Tetris tile-matching game as adopted by IBM PC. Even though Dear PyGui is not a game engine, it can easily handle graphical animations such as these. The source code is available in the Github repository.

TETRIS
Snake
Snake is a simple game with customisable settings for changing the speed and colours and fixing the snake length. Entirely made with Dear PyGui. The source code is available in the Github repository.

## https://github.com/hoffstadt/DearPyGui/wiki/Showcase-apps-older-Dear-PyGui-versions
Showcase apps older Dear PyGui versions
Raccoon edited this page on Nov 25, 2023 · 5 revisions

The following apps have been developed using older versions of Dear PyGui. The release of Dear PyGui version 1.0 included a few breaking changes, so that these apps are not compatible with the latest version. Since they do demonstrate the versatility of Dear PyGui, the applications are included here.
APPS MADE WITH DEAR PYGUI 0.6

The following apps were made with an older version of Dear PyGui (version 0.6) and are not compatible with the latest version of Dear PyGui. Still, they provide good examples of the type of apps that can be made with Dear PyGui.
A visual instrument for fiber analysis research

The fiber analysis tool is a scientific instrument used to determine local fiber volume fraction distribution in order to build accurate Finite Element Modelling simulations. In addition, it is used to determine the fiber volume fraction of manufactured parts. The source code is available in the GitLab repository.

Fiber analysis
MultiPy: organizing your Python scripts

MultiPy is a GUI application for Windows 10 that lets you conveniently keep a track of your python scripts for personal use or showcase by loading and grouping them into categories. It allows you to either run each script individually or together with just one click. The source code is available in the Github repository.

MultiPy
Text-to-speech dataset tools

Text to speech data set tools supports generating TTS datasets using audio and associated text automatically. Make cuts under a custom length. Uses Google Speech to text API to perform diarization and transcription or aeneas to force align text to audio. Transcribe audio via Google Speech to Text API with speaker separation (diarization). Quickly proofread and edit cuts. The tool is demonstrated in a YouTube video. The source code is available in the Github repository.

TTS-Tools
CoolName: Dataflow simulator

CoolName is a cycle-accurate, application-level static dataflow simulator, which can be used for analyzing high-level synthesis for application-specific hardware. CoolName can be used as a tool to compare and optimize dataflow graphs for application-specific hardware by reporting performance metrics such as latency, energy and utilization. For ease of use, the user can set input parameters, control the execution and gather performance results through the GUI. The source code is available in the Github repository.

CoolName
Interactive Assembly Line Balancer

The interactive assembly line balancer lets the user add multiple tasks and link them together to create and balance an assembly line by assigning tasks to various workstations to achieve the desired output rate with the smallest number of workstations according to the longest or shortest work element rule. This helps create well-balanced workloads for each workstation and minimizes bottlenecks. The app makes extensive use of the built-in node editor of Dear PyGui. The source code is available in the Github repository.

Line Balancer
Sarfis Pro: powerful distributed computing made easy

The goal of SARFIS Pro is to allow users to distribute any kind of compute task across multiple machines or even schedule a one-time task to run on all machines or specific machines, LAN and/or WAN. It will let people in CGI create render farms to use locally and/or in the cloud. Programmers can schedule tasks to compile software on multiple machines and run regression tests. Web designers can queue tasks that are too slow to be returned to the user in the request (such as exporting 10 years of banking data). For more information, check out the Sarfis Pro website.

Sarfis Pro
Planar Truss Element FEM Solver

This solver can be used to analyse planar (2 dimensional) truss element structures made of 1D bar elements connected at various nodes that include movement constraints and 1D forces acting at the nodes. A more detailed explanation and the source code can be found in the Github repo.

Solver Step 3
Drawing app

A simple drawing app that draws straight and dotted lines, rectangles, Bézier curves, freehand, circles and arrows. It offers the ability to undo/redo, save and open files and even has light/dark mode options. Check out the code in the Github repo.

SimpleDrawingApp
Python Digital Phosphor Display with RTLSDR (YouTube)

This video demonstrates an Intensity graded FFT or Python Digital Phosphor Display by Thomas Schucker. The accompanying blog post shows how to create a this dynamic graph. The code can be downloaded from the Github repo.

Python Digital Phospor GUI
Scientific apps made with Dear PyGui
Hyperspectral Imaging Acquisition

Hyperspectral Imaging (HSI) techniques have demonstrated potential to provide useful information in a broad set of applications in different domains, from precision agriculture to environmental science. A custom built system has been developed with Dear PyGui to control individual cameras and other devices and visualise data in order to perform hyperspectral imaging acquisition and analysis.

Hyperspectral Image Acquisition
Ultrasonic Tracking of Surgical Needle
Researchers at the School of Biomedical Engineering & Imaging Sciences, UCL and UCH have developed an ultrasonic surgical needle tracking technology which for the first time identifies the tip of a needle during surgeries. With ultrasonic tracking, a miniature fibre-optic ultrasound sensor is integrated within a thin needle to communicate with an external ultrasound imaging probe. The GUI was built using Dear PyGui, which was chosen for its real-time data acquisition and plotting abilities.