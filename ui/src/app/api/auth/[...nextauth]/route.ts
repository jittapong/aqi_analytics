import NextAuth from "next-auth"
import KeycloakProvider from "next-auth/providers/keycloak"

const handler = NextAuth({
  providers: [
    KeycloakProvider({
      clientId: process.env.KEYCLOAK_ID!,
      clientSecret: process.env.KEYCLOAK_SECRET!,
      issuer: process.env.KEYCLOAK_ISSUER,
    }),
  ],
  callbacks: {
    async jwt({ token, account, user }) {
      console.log("callbacks jwt")
      // if (account) {
      //   token.id = user?.id || user?.sub; // Keycloak's user ID
      // }
      return token;
    },
    async session({ session, token }) {
      console.log("callbacks session")
      // session.user.id = token.id; // Attach KEYCLOAK_ID to session
      return session;
    },
  },
})

export { handler as GET, handler as POST }

