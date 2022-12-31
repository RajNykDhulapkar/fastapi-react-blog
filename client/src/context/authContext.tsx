import axios from "axios";
import { createContext, useEffect, useState } from "react";

export interface IAuthenticationContext {
    currentUser: Object | null;
    login: (inputs: any) => Promise<void>;
    logout: () => Promise<void>;
}

export const AuthContext = createContext<IAuthenticationContext | null>(null);

export const AuthContextProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(
        JSON.parse(localStorage.getItem("user")) || null
    );

    const login = async (inputs: any) => {
        const params = new URLSearchParams();
        params.append("username", inputs.email);
        params.append("password", inputs.password);
        const res = await axios.post(import.meta.env.VITE_API_URL + "/api/auth/token", params, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });
        localStorage.setItem("access_token", res.data.access_token);
        const { data } = await axios.get(import.meta.env.VITE_API_URL + "/api/auth/me", {
            headers: {
                Authorization: `Bearer ${res.data.access_token}`,
            },
        });
        setCurrentUser((prevState) => ({
            ...prevState,
            ...data,
        }));
    };

    const logout = async () => {
        // await axios.post("/api/ping");
        setCurrentUser(null);
    };

    useEffect(() => {
        localStorage.setItem("user", JSON.stringify(currentUser));
    }, [currentUser]);

    return (
        <AuthContext.Provider value={{ currentUser, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
