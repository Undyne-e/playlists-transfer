import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import YandexLogin from './pages/YandexLogin';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/yandexlogin" element={<YandexLogin />} />
      </Routes>
    </Router>
  );
};

export default App;