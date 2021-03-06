# NewEgg Order Bot

A bot to automate checking and adding products to cart.

## How to run from executable (exe)

1. Login to [NewEgg's account settings page](https://secure.newegg.com/account/settings) from **Google Chrome**.
2. List NewEgg URL of products that you want to get in `productlist.txt`, one per line.
3. Run the program with `neweggbot.exe [delay in seconds]`

## How to run from source (non exe)

1. Install Python 3
2. Login to [NewEgg's account settings page](https://secure.newegg.com/account/settings) from **Google Chrome**.
3. List NewEgg URL of products that you want to get in `productlist.txt`, one per line.
4. Double click `run.bat`

## How to run from Python script (manual)

1. Install Python 3
2. Login to [NewEgg's account settings page](https://secure.newegg.com/account/settings) from **Google Chrome**.
3. List NewEgg URL of products that you want to get in `productlist.txt`, one per line.
4. (optional) Create and activate a virtual environment.
5. Install dependencies: `pip install -r requirements.txt`
6. Run the program: `python neweggbot.py [delay in seconds]`

Note: Delay in seconds is optional, defaults to 1 second. This might prevent temporary bans due to rapid requests.

## Issues

Please report any issues using GitHub's issue tracker.

## Disclaimer

This program is provided as proof of concept, for educational purposes only. I am not responsible for any damages that may be caused by misuse of the program.
