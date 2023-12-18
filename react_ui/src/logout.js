import { useNavigate } from 'react-router-dom';

const Logout = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('_a');

        navigate('/login/');
    };

    handleLogout();

    return null;
}
export default Logout;
