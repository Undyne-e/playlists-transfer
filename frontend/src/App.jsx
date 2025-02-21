import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import YandexLogin from './pages/Yandex/YandexLogin';
import YandexCallback from './pages/Yandex/YandexCallback';
import ActivateAccount from './pages/ActivateAccount';
import ActivatePrompt from './pages/ActivatePrompt';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/yandexlogin" element={<YandexLogin />} />
        <Route path="/yandexcallback" element={<YandexCallback />} />
        <Route path="/auth/activate/:uid/:token/" element={<ActivateAccount />} />
        <Route path="/activateprompt" element={<ActivatePrompt />} />
      </Routes>
    </Router>
  );
};

export default App;