import React, { createContext, useState, useContext } from "react";

type UserContextType = {
  username: string | null;
  setUsername: (username: string | null) => void;
};

const UserContext = createContext<UserContextType>({
  username: null,
  setUsername: () => {},
});

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [username, setUsername] = useState<string | null>(null);

  return (
    <UserContext.Provider value={{ username, setUsername }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUserContext = () => useContext(UserContext);
