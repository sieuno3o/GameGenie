import defaultDashboard from "@/layout/dashboard/DefaultDashboard";

const MainSearchPage = () => import("@/views/MainSearchPage.vue");

const defaultRoutes = [
  {
    path: "",
    component: defaultDashboard,
    children: [
      {
        path: "",
        name: "main",
        component: MainSearchPage,
      },
    ]
    }
]

export default defaultRoutes;