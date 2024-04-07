import React, { useState, useEffect } from 'react';
import { FaRobot } from "react-icons/fa6";

const ChatApp = () =>
{
    const [messages, setMessages] = useState([]);
    const [userMessage, setUserMessage] = useState('');
    const [welcomeMessageShown, setWelcomeMessageShown] = useState(false);


    useEffect(() =>
    {
        if (!welcomeMessageShown)
        {
            const welcomeMessage = {
                text: "Greetings! I'm Chatbot, here to assist you. Feel free to ask me anything.",
                sender: 'chatbot',
                time: getCurrentTime(),
            };
            setMessages([welcomeMessage, ...messages]);
            setWelcomeMessageShown(true);
        }
    }, []);

    const getCurrentTime = () =>
    {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    };

    const sendMessage = () =>
    {
        if (!userMessage.trim()) return;

        const newUserMessage = { text: userMessage, sender: 'user', time: getCurrentTime() };
        const newMessages = [...messages, newUserMessage];
        setMessages(newMessages);
        setUserMessage('');

        fetch('http://localhost:5000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        })
            .then((res) => res.json())
            .then((data) =>
            {
                const responseMessage = { text: data.response, sender: 'chatbot', time: getCurrentTime() };
                setMessages([...newMessages, responseMessage]);
            })
            .catch((error) =>
            {
                console.error('Error sending message:', error);
            });
    };

    const handleSubmit = (e) =>
    {
        e.preventDefault();
        sendMessage();
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center container">
                <div className="col-lg-6 h-100">
                    <div className="card h-100">
                        <div className="card-header bg-light text-black " style={{ fontSize: '20px' }}> <FaRobot style={{ fontSize: '40px', marginRight: '10px' }} />Chat Bot</div>
                        <div className="card-body" style={{ maxHeight: '60vh', minHeight: '67vh', overflowY: 'scroll' }}>
                            <div className="chat-container" >
                                {messages.map((message, index) => (
                                    <div
                                        key={index}
                                        className={`chat-message d-flex flex-column ${message.sender === 'chatbot' ? 'justify-content-start align-items-start' : 'justify-content-end align-items-end'}`}
                                    >
                                        <p className={`bg-${message.sender === 'chatbot' ? 'primary' : 'secondary'} text-white rounded px-3 py-2 mb-1`}>{message.text}</p>
                                        <span className="text-muted">{message.time}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <form onSubmit={handleSubmit}>
                            <div className="input-group mb-3">
                                <input
                                    type="text"
                                    className="form-control"
                                    placeholder="Type your message..."
                                    value={userMessage}
                                    onChange={(e) => setUserMessage(e.target.value)}
                                />
                                <button className="btn btn-primary" type="submit">Send</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatApp;
