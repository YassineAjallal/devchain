const elBtnMetamask = document.getElementById('auth-metamask');
const csrf_token = JSON.parse(document.getElementById('csrf_token').textContent);

const handleApiPost = async (endpoint, params) => {
    const result = await axios.post(`${endpoint}`, params, {
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf_token
        },
    });
    return result.data;
};

const requestMessage = (account, chain) =>
    handleApiPost('http://127.0.0.1:8000/request', {
        address: account,
        chain: chain,
        network: 'evm',
    });

const verifyMessage = (message, signature) =>
    handleApiPost('http://127.0.0.1:8000/verify', {
        message: message,
        signature: signature,
        network: 'evm',
    });


const connectToMetamask = async () => {
    const provider = new ethers.providers.Web3Provider(window.ethereum, 'any');

    const [accounts, chainId] = await Promise.all([
        provider.send('eth_requestAccounts', []),
        provider.send('eth_chainId', []),
    ]);

    const signer = provider.getSigner();
    return { signer, chain: chainId, account: accounts[0] };
};

const handleAuth = async () => {
    const { signer, chain, account } = await connectToMetamask();

    if (!account) {
        throw new Error('No account found');
    }
    if (!chain) {
        throw new Error('No chain found');
    }

    const { message } = await requestMessage(account, chain);
    const signature = await signer.signMessage(message);
    await verifyMessage(message, signature);
    location.reload()
};

function init() {
    elBtnMetamask.addEventListener('click', async () => {
        handleAuth().catch((error) => console.log(error));
    });
}

window.addEventListener('load', () => {
    init();
});