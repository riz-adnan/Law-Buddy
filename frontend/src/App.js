import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState([]);
  const [answer, setAnswer] = useState('');

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };
  let flag=false;
  useEffect(() => {
  const initial = async () => {
    try {
      const response = await axios.get('http://localhost:5000/get_ipc');
      setResult(response.data.result);
     
    } catch (error) {
      console.error('Error processing query:', error);
    }}
    initial();
  },[])
  const handleProcessQuery = async () => {
    try {
      console.log('hi');
      const response = await axios.post('http://localhost:5000/process_query', {
        question: query,
      });
      flag=true;
      console.log(response.data);
      setResult(response.data.result);
      setAnswer(response.data.answer);
    } catch (error) {
      console.error('Error processing query:', error);
    }
  };
  

  return (
    <div className="App">
      <h1>Law buddy</h1>
      <div>
        <label>Enter your Query:</label>
        <input type="text" value={query} onChange={handleQueryChange} />
        <button onClick={handleProcessQuery}>Process Query</button>
      </div>
      <div>
      <div>
        <h2>AI answer for your query:</h2>
        <p>{answer}</p>
      </div>
        <h2>Relevant sections for you query:</h2>
        <ul>
          {result.map((section, index) => (
           
            <li key={index}><h3>{section.substr(14,16)}</h3>{section}</li>
          ))}
       </ul>
      </div>
      
    </div>
  );
}

export default App;
