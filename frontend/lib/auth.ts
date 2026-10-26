import { NextAuthOptions } from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import AzureADProvider from "next-auth/providers/azure-ad";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions: NextAuthOptions = {
  providers: [
    ...(process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET
      ? [
          GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET,
          }),
        ]
      : []),
    ...(process.env.AZURE_AD_CLIENT_ID && process.env.AZURE_AD_CLIENT_SECRET
      ? [
          AzureADProvider({
            clientId: process.env.AZURE_AD_CLIENT_ID,
            clientSecret: process.env.AZURE_AD_CLIENT_SECRET,
            tenantId: process.env.AZURE_AD_TENANT_ID || "common",
          }),
        ]
      : []),
    CredentialsProvider({
      id: "demo-teacher",
      name: "School Account",
      credentials: {
        email: { label: "School Email", type: "email", placeholder: "teacher@district.k12.us" },
        name: { label: "Teacher Name", type: "text", placeholder: "Ms. Robinson" },
      },
      async authorize(credentials) {
        if (!credentials?.email) {
          return {
            id: "teacher_demo_01",
            name: "Demo Math Educator",
            email: "educator@openmathforge.org",
            role: "teacher",
            tier: "pro",
            district: "Lincoln Unified School District",
          };
        }
        return {
          id: `teacher_${Buffer.from(credentials.email).toString("hex").slice(0, 12)}`,
          name: credentials.name || credentials.email.split("@")[0],
          email: credentials.email,
          role: "teacher",
          tier: "pro",
          district: credentials.email.includes("@") ? credentials.email.split("@")[1] : "Independent",
        };
      },
    }),
  ],
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60,
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = (user as any).role || "teacher";
        token.tier = (user as any).tier || "pro";
        token.district = (user as any).district || "School District";
      }
      return token;
    },
    async session({ session, token }) {
      if (session?.user) {
        (session.user as any).role = token.role || "teacher";
        (session.user as any).tier = token.tier || "pro";
        (session.user as any).district = token.district || "School District";
      }
      return session;
    },
  },
  secret: process.env.NEXTAUTH_SECRET || "openmathforge-dev-secret-key-change-in-prod-32bytes",
};

