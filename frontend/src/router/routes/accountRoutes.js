import defaultDashboard from "@/layout/dashboard/DefaultDashboard";

const LoginPage = () => import("@/views/account/LoginPage.vue");
const SignupPage = () => import("@/views/account/SignupPage.vue");
const SuccessSignup = () => import("@/views/account/SuccessSignup.vue");

const accountRoutes = [
  {
    path: "",
    component: defaultDashboard,
    children: [
      {
        path: "login",
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
      {
        path: "success",
        name: "success_signup",
        component: SuccessSignup,
      },
    ],
  }, 
];

export default accountRoutes;
