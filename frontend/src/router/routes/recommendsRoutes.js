import defaultDashboard from "@/layout/dashboard/DefaultDashboard.vue";

const RecommendPage = () => import("@/views/RecommendPage.vue");

const recommendationsRoutes = [
  {
    path: "",
    component: defaultDashboard,
    children: [
      {
        path: "",
        name: "recommends",
        component: RecommendPage,
      },
    ],
  },
];

export default recommendationsRoutes;
