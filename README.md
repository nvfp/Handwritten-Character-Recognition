# Handwritten-Character-Recognition

This software was made to show the beauty of neural networks, visualizing the fully connected neural network diagram, and how it's being trained. Built from the ground up without any machine learning libraries.

![Demo gif](_imgs/demo.gif)

- What we can do
    1. Create a new network
    2. Create datasets
    3. Train the model
    4. Save the network and reopen it
    5. View and delete our own datasets

- Customization
    - Change the number of hidden layers
    - Change the drawing pad resolution

- **The main visual interface**

    ![The main visual interface of the application](_imgs/1.jpg)

- **Dataset viewer**

    ![Dataset viewer](_imgs/2.jpg)

- **Training the network**

    ![Training the network](_imgs/3.jpg)

> **[Demo video](https://youtu.be/GX0xBjiwgtg)**.


## Installation

1. Download the latest [version](https://github.com/nvfp/Handwritten-Character-Recognition/releases)
2. Save it under your favorite folder (e.g. `/foo/Handwritten-Character-Recognition`)
3. Navigate to `/foo/Handwritten-Character-Recognition`
4. Install dependencies by running `pip install -r requirements.txt`
5. Run `python __main__.py`
6. There you go!


## FAQ

- **To exit the application**: press the "esc" key

- **To reset the network**:

    Search for `NN_NEW` in `__main__.py` and set it to `True`. After you trained the network, press the button "save" to save it.

- **To reset the dataset**:

    Example: to reset the dataset of zero "0", replace the contents of the file `dataset/0.json` with an empty list `[]`.


## Limitations

- Always in fullscreen mode
- The UI layout is customized for the 1366x768 display size


## Troubleshoot

- To report bugs/issues or ask questions, you can reach me [here](https://nvfp.github.io/contact) or open an issue/pull request.


## Changelog

- 1.1.0 (June 11, 2023):
    - removed `carbon_plug`, using [mykit](https://github.com/nvfp/mykit) instead
- v1.0.1 (May 10, 2023):
    - BUG FIXED: Renamed `carbon` to `carbon_plug` to prevent conflicts with the original `carbon` module (if installed).


## License

This project is licensed under the MIT license.
