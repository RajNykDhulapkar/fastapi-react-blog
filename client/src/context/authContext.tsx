import axios from "axios";
import { createContext, useEffect, useState } from "react";

export interface IAuthenticationContext {
    currentUser: Object | null;
    logIn: () => void;
    logOut: () => void;
}

export const AuthContext = createContext<IAuthenticationContext | null>(null);

export const AuthContextProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(
        JSON.parse(localStorage.getItem("user")) || null
    );

    const login = async (inputs: any) => {
        const res = await axios.post("/api/auth/login", inputs);
        setCurrentUser((prevState) => ({
            ...prevState,
        }));
    };

    const logout = async (inputs: any) => {
        await axios.post("/api/auth/logout");
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
