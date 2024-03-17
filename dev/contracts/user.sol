// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract User
{
    struct Infos
    {
        string name;
        string password;
    }

    mapping(string => Infos) private users;

    function addUser(string memory _name, string memory _password) public {
        require(bytes(_name).length > 0, "Error: name is empty");
        require(bytes(_password).length > 0, "Error: password is empty");
        
        users[_name].name = _name;
        users[_name].password = _password;
    }
    
}