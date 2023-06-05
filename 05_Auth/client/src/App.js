import {useEffect, useState} from "react";
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  // useEffect(()=>{
  //   fetch("/check_login")
  //   .then(r => r.json())
  //   .then(user => setUser(user))
  // },[])

  function handleSubmit(e){
    e.preventDefault();
    fetch("/signin", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({name: name, password: password})
    })
    .then(res => res.json())
    .then(data => setUser(data))

  }
    

  function handleLogout(e){
    e.preventDefault()
    fetch("/logout", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(setUser(null))
  }


  function handleUsername(e){
    setName(e.target.value)
  }

  function handlePassword(e){
    setPassword(e.target.value)
  }
  if(user){
    return (
      <>
      <h1>Welcome, {user.name}</h1>
        <form onSubmit={handleLogout}>
          <button type="submit">Logout</button>
        </form>
      </>
    )
  }
  else{
    return (
      <>
      <form onSubmit={handleSubmit}>
        <h2>Username</h2>
        <input type="text" value={name} onChange={handleUsername}/>
        <h2>Password</h2>
        <input type="text" value={password} onChange={handlePassword}/>
        
         <button type="submit">Login</button>
      </form>
      </>
    );
  }
}

export default App;
