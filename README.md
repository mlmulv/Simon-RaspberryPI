<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
         <li><a href="#Thonny">Thonny</a></li>
        <li><a href="#altium">Altium</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#authors">Authors</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

In this project we are going to recreate the popular game called "Simon" using a Raspberry Pi Pico. This will be done by uploading a python file from Thonny to a Raspberry Pi Pico that has been flashed with MicroPython. The game will be all be assembled on a PCB.

[Demo of Simon on PCB](https://www.dropbox.com/scl/fi/wlp0poy3fge87f9is8fu8/IMG_6259.MOV?rlkey=6hiw2l3pcr1uelsrrb8k62q38&dl=0)

<!-- GETTING STARTED -->
## Getting Started

To get started with the project you will need to follow the following instructions.

### Installation

*  Clone the repo
   ```sh
   git clone https://github.com/mlmulv/Simon-RaspberryPI
   ```
### Thonny

1. Install Thonny on your machine.
2. If you have not flashed MicroPython on your Raspberry Pi Pico you will need to. (https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)
3. Connect your Raspberry Pi Pico to your machine.
4. Load the python file onto your Raspberry Pi Pico.

### Alitum
1. If you have not used Altium before you will need to create an account and obtain a license.
2. Create an Altium Project.
3. Add the Schematic and PCB file to your project.


<!-- USAGE EXAMPLES -->
## Usage

1. Make sure you completed all the steps in the Installation section.
2. In the **Simon.py** file, I layout all the code needed. You can customize the code how you would like. In my case, there are  3 levels: easy, medium, and hard. The easy level has 5 sequences, the medium level has 10 sequences, and the hard level has 15 sequences. You can also adjust the amount of times before sequences within the interrupt for each button.
4. The PCB is fit for the current parts I have. You can adjust any of the parts, size, or orientation to your liking. Currently, the PCB is quite large so I would recommend to maybe size down if possible. Take into account the LEDs are surface mount, so make sure that works with your current inventory.
5. After you get back your PCB, you can solder everything and connect your Rasberry Pi Pico to a power source and Simon should be all set to go.


<!-- Authors -->
## Authors

Markus Mulvihill - [LinkedIn](https://www.linkedin.com/in/markus-mulvihill-6549961a0/) 

Project Link: (https://github.com/mlmulv/Simon-RaspberryPI)
