// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract Articles
{
    struct Infos {
        string title;
        string content;
        uint256 timestamp;
    }

    mapping(address => Infos[]) articles;

    function addArticle(string memory title, string memory content, uint256 timestamp) public {
        Infos memory article = Infos(title, content, timestamp);
        articles[msg.sender].push(article);
    }


}



