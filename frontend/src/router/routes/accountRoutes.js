import defaultDashboard from "@/layout/dashboard/DefaultDashboard";

const LoginPage = () => import("@/views/account/LoginPage.vue");
const SignupPage = () => import("@/views/account/SignupPage.vue");
const ProfilePage = () => import("@/views/account/ProfilePage.vue");

const accountRoutes = [
  {
    path: "login",
    component: defaultDashboard,
    children: [
      {
        path: "",
        name: "login",
        component: LoginPage,
      },
    ],
  },
  {
    path: "signup",
    component: defaultDashboard,
    children: [
      {
        path: "",
        name: "signup",
        component: SignupPage,
      },
    ],
  },
];

export default accountRoutes;
