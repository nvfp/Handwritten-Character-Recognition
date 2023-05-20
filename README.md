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

1. Download this repo and save it to your machine (e.g. `~/code/Handwritten-Character-Recognition`)
2. Go to the folder where `Handwritten-Character-Recognition` is located, run:

    ```sh
    python Handwritten-Character-Recognition
    ```


## FAQ

- **To exit the application**: press the "esc" key

- **To reset the network**:

    Search for `NN_NEW` in `__main__.py` and set it to `True`. After you trained the network, press the button "save" to save it.

- **To reset the dataset**:

    Example: to reset the dataset of zero "0", replace the contents of the file `dataset/0.json` with an empty list `[]`.


## Troubleshoot

- If the `numpy` or `numba` module is missing, run the following command:

    ```sh
    pip install -r requirements.txt
    ```
- To report bugs/issues or ask questions, you can reach me [here](https://nvfp.github.io/contact) or open an issue/pull request.


## Changelog

- v1.0.1 (May 10, 2023):
    - BUG FIXED: Renamed `carbon` to `carbon_plug` to prevent conflicts with the original `carbon` module (if installed).


## License

This project is licensed under the MIT license.
