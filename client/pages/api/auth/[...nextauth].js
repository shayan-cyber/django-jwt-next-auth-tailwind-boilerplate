import NextAuth from "next-auth"

import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions = {
    // Configure one or more authentication providers
    providers: [
        CredentialsProvider({
            // The name to display on the sign in form (e.g. 'Sign in with...')
            name: "Credentials",
            // The credentials are used to generate a suitable form on the sign in page.
            // You can specify whatever fields you are expecting to be submitted.
            // e.g. domain, username, password, 2FA token, etc.
            // You can pass any HTML attribute to the <input> tag through the object.
            credentials: {
                username: {
                    label: "Username",
                    type: "text",
                    placeholder: "John",
                },
                email: {
                    label: "Email",
                    type: "email",
                    placeholder: "johndoe@email.com",
                },
                password: { label: "Password", type: "password" },
            },
            async authorize(credentials, req) {
        
                try {
                  const res = await fetch("http://localhost:8000/auth/signin/", {
                    method: "POST",
                    body: JSON.stringify({
                      username:credentials.username,
                      email: credentials.email,
                      password: credentials.password,
                    }),
                    headers: { "Content-Type": "application/json" },
                  });
        
                  if (!res.ok) {
                    // credentials are invalid
                    return null;
                  }
        
                  const parsedResponse = await res.json();
        
                  // accessing the jwt returned by server
                  const jwt = parsedResponse.access;
        
        // You can make more request to get other information about the user eg. Profile details
        
                 // return user credentials together with jwt
                  return {
                    ...credentials,
                    jwt,
                  };
                } catch (e) {
                  return null;
                }
              },
        }),
    ],
    

      callbacks: {
        jwt: async ({ token, user }) => {
         // user is only available the first time a user signs in authorized
          if (user) {
            return {
              ...token,
              jwt: user.jwt,
            };
          }
          return token;
        },
        session: async ({ session, token }) => {
          if (token) {
            session.jwt = token.jwt;
          }
          return session;
        },
      },
};

export default NextAuth(authOptions);