import defaultDashboard from "@/layout/dashboard/DefaultDashboard";

const MainPage = () => import("@/views/MainPage.vue");

const defaultRoutes = [
  {
    path: "",
    component: defaultDashboard,
    children: [
      {
        path: "",
        name: "main",
        component: MainPage,
      },
    ]
    }
]

export default defaultRoutes;