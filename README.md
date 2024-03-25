# DevChain - DApp Blogger

DevChain is a decentralized application (DApp) for blogging, built with Django framework for the backend. It utilizes smart contracts written in Solidity for managing blog posts. Interaction with the smart contract is facilitated through Web3.py library. Brownie framework is used for deploying the smart contract, while Ganache is used for local blockchain testing.

## Features
- User authentication
- Creating, reading, updating, and deleting blog posts.
- Interaction with Ethereum blockchain through smart contracts.
- Seamless deployment and testing of smart contracts using Brownie and Ganache.
- Enhanced security through decentralized architecture.

## Technologies Used
- Django: A high-level Python web framework for rapid development.
- Solidity: A contract-oriented programming language for writing smart contracts on the Ethereum blockchain.
- Web3.py: A Python library for interacting with Ethereum.
- Brownie: A Python-based development and testing framework for Ethereum smart contracts.
- Ganache: A personal blockchain for Ethereum development.

## Prerequisites
- Install MetaMask extension in your web browser.
- Create a `.env` file in the root directory of the project

## Installation
1. Clone this repository in your Desktop:
    ```
    git clone https://github.com/YassineAjallal/devchain.git
    cd devchain
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Install Ganache CLI using npm:
    ```
    npm install -g ganache-cli
    ```
4. Start Ganache CLI in a separate terminal:
    ```
    ganache-cli
    ```
5. cd to the blockchain directory and run the Brownie deployment script:
    ```
    cd blockchain
    brownie run scripts/deploy.py
    ```
6. Copy the contract address and paste it as ARTICLES_CONTRACT_ADDRESS variable in the .env file:
    ```
    ARTICLES_CONTRACT_ADDRESS=your_contract_address
    ```
7. Add your Moralis API key to the .env file:
    ```
    API_KEY=your_api_key
    ```
8. Visit [this link](https://www.geeksforgeeks.org/how-to-set-up-ganche-with-metamask/) to connect MetaMask with the Ganache network.
9. cd to the backend directory and run the Django server:
    ```
    cd backend
    python manage.py runserver
    ```
10. Access the application via your web browser at [http://localhost:8000](http://localhost:8000).

## Usage
1. Register an account or log in if you already have one.
2. Create, view, update, or delete blog posts.
3. Interact with the Ethereum blockchain to store and retrieve blog post data.
4. Experiment with local blockchain deployment and testing using Ganache and Brownie.

## Acknowledgements
Thanks to the Django, Solidity, Web3.py, Brownie, and Ganache communities for providing excellent frameworks and tools for building decentralized applications.
