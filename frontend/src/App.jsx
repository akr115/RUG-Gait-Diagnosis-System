import { Routes, Route } from 'react-router-dom';
import Home from './components/diagnosis-table/Home';
import './App.css';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
    </Routes>
  );
}
