import RecommendDashBoard from "@/layout/dashboard/RecommendDashBoard.vue";

const RecommendPage = () => import("@/views/RecommendPage.vue");

const recommendationsRoutes = [
  {
    path: "",
    component: RecommendDashBoard,
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
