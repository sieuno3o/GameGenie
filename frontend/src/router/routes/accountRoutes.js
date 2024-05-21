import defaultDashboard from "@/layout/dashboard/DefaultDashboard";

const LoginPage = () => import("@/views/account/LoginPage.vue");
const SignupPage = () => import("@/views/account/SignupPage.vue");

const accountRoutes = [
  {
    path: "",
    component: defaultDashboard,
    children: [
      {
        path: "/login",
        name: "login",
        component: LoginPage,
      },
      {
        path: "/signup",
        name: "sigunup",
        component: SignupPage,
      },
    ],
  }, 
];

export default accountRoutes;
