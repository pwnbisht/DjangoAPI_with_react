import React, {useState} from 'react';
import "./style.css";
import axios from 'axios';
import config from "./config";
import refreshToken from "./refresh";
import {useNavigate} from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [file3, setFile3] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  let [error, setError] = useState("");
  let [success, setSuccess] = useState("");

  const handleLogout = () => {
    localStorage.removeItem('_a');
    localStorage.removeItem('_r');

    navigate('/login/');
  };

  const baseURL = config.baseURL;
  let uploadingEndpoint = "files/uploads/";
  const handleFileChange = (fileNumber, event) => {
    const selectedFile = event.target.files[0];

    // Set the appropriate file state based on the fileNumber
    switch (fileNumber) {
      case 1:
        setFile1(selectedFile);
        break;
      case 2:
        setFile2(selectedFile);
        break;
      case 3:
        setFile3(selectedFile);
        break;
      default:
        break;
    }
  };
  const handleUpload = async (e) => {
  e.preventDefault();
  setSuccess("");
  setError("");
  if (!file1 && !file2 && !file3) {
    setError("Please select at least one file before submitting.");
    return;
  }
  try {
    setIsUploading(true);

    const formData = new FormData();
    file1 && formData.append('file1', file1);
    file2 && formData.append('file2', file2);
    file3 && formData.append('file3', file3);

    let accessToken = localStorage.getItem('_a');

    let response = await axios.post(
      `${baseURL}${uploadingEndpoint}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (response.status === 201) {
      setSuccess('File Uploaded Successfully');
      setError("");
    }
    setFile1(null);
    setFile2(null);
    setFile3(null);
  } catch (error) {
    e.preventDefault();
    if (error.response && error.response.status === 401) {
      await refreshToken();
      await handleUpload(e); // Pass the event to retry the upload
    } else if (error.response && error.response.status === 400) {
      setError(error.response.data.errors.non_field_errors[0]);
    }
  } finally {
    setIsUploading(false);
  }
};
  return (
      <div className="background">
        <div className="shape"></div>
        <div className="shape"></div>
        <form>
          <h1>Upload File</h1>
          {success &&
              <p style={{color: "green", fontSize: "15px", marginTop: "30px", textAlign: "center"}}>{success}</p>}
          {error && <p style={{color: "red", fontSize: "15px", marginTop: "30px", textAlign: "center"}}>{error}</p>}
          <div>
            <input type="file" onChange={(e) => handleFileChange(1, e)}/>
          </div>
          <div>
            <input type="file" onChange={(e) => handleFileChange(2, e)}/>
          </div>
          <div>
            <input type="file" onChange={(e) => handleFileChange(3, e)}/>
          </div>
          <button onClick={handleUpload}>Submit</button>
          <div className="social">
            <button style={{background:'red', color:'white'}} onClick={handleLogout}>Logout</button>
          </div>
        </form>

        {isUploading && (
            <div className="overlay">
              <div className="loader"></div>
            </div>
        )}
      </div>
  );
};

export default Home;
