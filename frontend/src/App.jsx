import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import YandexCallback from './pages/Yandex/YandexCallback';
import ActivateAccount from './pages/ActivateAccount';
import ActivatePrompt from './pages/ActivatePrompt';
import AccountSettings from './pages/AccountSettings';
import Logout from './pages/Logout';
import DeleteAccount from './pages/DeleteAccount';
import Home from './pages/Home';
import GoogleCallback from './pages/Google/GoogleCallback';
import YandexSavePlaylists from './pages/Yandex/YandexSavePlaylists';
import PlaylistTransfer from './pages/PlaylistTransfer';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/yandexcallback" element={<YandexCallback />} />
        <Route path="/auth/activate/:uid/:token/" element={<ActivateAccount />} />
        <Route path="/activateprompt" element={<ActivatePrompt />} />
        <Route path="/accountsettings" element={<AccountSettings />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/deleteaccount" element={<DeleteAccount />} />
        <Route path="/home" element={<Home />} />
        <Route path="/googlecallback" element={<GoogleCallback />} />
        <Route path="/yandex/saveplaylists" element={<YandexSavePlaylists />} />
        <Route path="/playlisttransfer" element={<PlaylistTransfer />} />
      </Routes>
    </Router>
  );
};

export default App;