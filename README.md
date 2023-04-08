## Handwritten-Character-Recognition
Let's have a look at how a neural network looks. This is a from-scratch neural network implemented in Python using numpy and numba, designed to recognize handwritten characters. The network diagram displays a few out of thousands of inputs. Blue color is used to represent positive neurons and weights, while red is used for the negative ones.

### The main visual interface
![The main visual interface of the application](_imgs/1.jpg)

### Dataset viewer
![Dataset viewer](_imgs/2.jpg)

### Training the network
![Training the network](_imgs/3.jpg)

### [Demo video](https://youtu.be/GX0xBjiwgtg).

## Usage
1. Download this repository and save it to your machine (e.g. ~/code/Handwritten-Character-Recognition)
2. Navigate to the folder where `Handwritten-Character-Recognition` is located, then run the following command:
    ```sh
    python Handwritten-Character-Recognition
    ```

## FAQ
### 1. How to exit the application?
Press the "esc" key to exit.

### 2. How to reset the network?
Search for "NN_NEW" in `__main__.py` and set it to `True`, and after you trained the network, press the button "save" to save it.

### 3. How to reset the dataset?
Suppose you wish to reset the dataset of zero "0". In that case, replace all the contents inside the file `dataset/0.json` with an empty list `[]`.

## Troubleshoot
1. If the "numpy" or "numba" module is missing, run the following command:
    ```sh
    pip install -r requirements.txt
    ```

## License
This project is licensed under the MIT license.
