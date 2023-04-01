import React, { useEffect, useRef, useState } from 'react';
import {
  ChatContainer,
  MessageList,
  MessageInput,
  Message,
  Avatar,
  TypingIndicator,
} from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { PrivateWrapper } from '../components/layouts';
import { searchQuery } from '../api/Bot';
import BotAvatar from '../assets/images/bot.png';
import UserAvatar from '../assets/images/user.png';

// Main Home Page
const Home = () => {
  const inputRef = useRef();
  const [messages, setMessages] = useState([]);
  const [msgInputValue, setMsgInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSendMessage = async (text) => {
    // Add user's message to message list
    const newMessage = { type: 'text', message: text, sender: 'user', direction: 'outgoing' };
    setMessages((ps) => [...ps, newMessage]);

    setMsgInputValue('');
    inputRef.current.focus();
    setIsTyping(true);
    // Send message to search API and add bot's response to message list
    const botResponse = await searchQuery(text);

    const botMessage = {
      type: 'text',
      message: botResponse.message,
      sender: 'bot',
      direction: 'incoming',
    };
    setMessages((ps) => [...ps, botMessage]);
    setIsTyping(false);
  };

  useEffect(() => {
    // TODO: Load message from db
    if (messages.length === 0) {
      setMessages((ps) => [
        ...ps,
        {
          type: 'text',
          message: 'Hello 👋, I am a health care bot. How may I assist you today?',
          sender: 'bot',
          direction: 'incoming',
        },
      ]);
    }
  }, []);

  return (
    <PrivateWrapper pageName="MediCare Bot">
      <div
        style={{
          height: '90vh',
          width: '100%',
        }}
      >
        <ChatContainer>
          <MessageList
            style={{ paddinTop: 20 }}
            typingIndicator={isTyping && <TypingIndicator content="Bot is typing" />}
          >
            {messages.map((message) => (
              <Message model={message} avatarPosition={message.sender === 'bot' ? 'tl' : 'tr'}>
                {message.sender === 'bot' ? (
                  <Avatar src={BotAvatar} name="Bot" size="sm" status="available" />
                ) : (
                  <Avatar src={UserAvatar} name="You" size="sm" />
                )}
              </Message>
            ))}
          </MessageList>
          <MessageInput
            placeholder="Type message here"
            onSend={handleSendMessage}
            onChange={setMsgInputValue}
            value={msgInputValue}
            ref={inputRef}
          />
        </ChatContainer>
      </div>
    </PrivateWrapper>
  );
};

export default Home;
