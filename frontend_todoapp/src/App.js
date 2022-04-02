import{
  HashRouter as Router,
  Routes,
  Link,
  Route
} from 'react-router-dom';

import './App.css';

import TasksListPage from './pages/TasksListPage'


function App() {
  return (
    <Router>
      <div>
      <Routes>
        <Route path="/" element={<TasksListPage/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
