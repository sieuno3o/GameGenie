import defaultDashboard from "@/layout/dashboard/DefaultDashboard";

const RecommendationsPage = () => import("@/views/recommendations/RecommendationsPage.vue");

const recommendationsRoutes = [
  {
    path: "",
    component: defaultDashboard,
    children: [
      {
        path: "recommendations",
        name: "recommendations",
        component: RecommendationsPage,
      },
    ],
  },
];

export default recommendationsRoutes;
