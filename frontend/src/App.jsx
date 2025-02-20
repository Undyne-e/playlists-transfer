import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import YandexLogin from './pages/Yandex/YandexLogin';
import YandexCallback from './pages/Yandex/YandexCallback';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/yandexlogin" element={<YandexLogin />} />
        <Route path="/yandexcallback" element={<YandexCallback />} />
      </Routes>
    </Router>
  );
};

export default App;