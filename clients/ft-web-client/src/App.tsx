import * as React from 'react';
import './App.css';
import DemoComponent from './components/demoComponent'

import logo from './logo.svg';

class App extends React.Component {
  public render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.tsx</code> and save to reload.
        </p>
        <DemoComponent fmulp="Johnny" onLaserButtonClick={() => console.log("Lasers Activated Callback") } />
      </div>
    );
  }
}

export default App;