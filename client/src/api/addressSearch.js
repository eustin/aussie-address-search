import axios from "axios";

const instance = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL,
});

const httpPostSearch = async (value) => {
  try {
    const response = await instance.post("/search", { searchInput: value });
    return response.data;
  } catch (error) {
    console.log(error);
    throw error;
  }
};

export { httpPostSearch };
