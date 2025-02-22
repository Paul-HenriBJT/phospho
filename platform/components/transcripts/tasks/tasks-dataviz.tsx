import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { authFetcher } from "@/lib/fetcher";
import { dataStateStore, navigationStateStore } from "@/store/store";
import { useUser } from "@propelauth/nextjs/client";
import Link from "next/link";
import React from "react";
import { useEffect, useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import useSWR from "swr";

import { Button } from "../../ui/button";
import { Skeleton } from "../../ui/skeleton";

interface NbDailyTasks {
  day: string;
  date: string;
  nb_tasks: number;
}

interface EventsRanking {
  event_name: string;
  nb_events: number;
}

interface SuccessRate {
  day: string;
  date: string;
  success_rate: number;
}

interface SuccessRateByPosition {
  task_position: number;
  success_rate: number;
}

interface TasksMetrics {
  total_nb_tasks: number;
  global_success_rate: number;
  most_detected_event: string;
  nb_daily_tasks: NbDailyTasks[];
  events_ranking: EventsRanking[];
  daily_success_rate: SuccessRate[];
  success_rate_per_task_position: SuccessRateByPosition[] | null;
}

const TasksDataviz: React.FC = () => {
  const { accessToken } = useUser();

  const tasksColumnsFilters = navigationStateStore(
    (state) => state.tasksColumnsFilters,
  );

  const hasSessions = dataStateStore((state) => state.hasSessions);

  const selectedProject = navigationStateStore(
    (state) => state.selectedProject,
  );
  const project_id = selectedProject?.id;

  let flagFilter: string | null = null;
  let eventFilter: string | null = null;
  for (let filter of tasksColumnsFilters) {
    if (
      filter.id === "flag" &&
      (typeof filter?.value === "string" || filter?.value === null)
    ) {
      flagFilter = filter?.value;
    }
    if (
      filter.id === "events" &&
      (typeof filter?.value === "string" || filter?.value === null)
    ) {
      eventFilter = filter?.value;
    }
  }

  const { data: totalNbTasksData } = useSWR(
    [
      `/api/explore/${project_id}/aggregated/tasks`,
      accessToken,
      flagFilter,
      eventFilter,
      "total_nb_tasks",
    ],
    ([url, accessToken]) =>
      authFetcher(url, accessToken, "POST", {
        metrics: ["total_nb_tasks"],
        tasks_filter: {
          flag: flagFilter,
          event_name: eventFilter,
        },
      }),
  );
  const totalNbTasks: number | null | undefined =
    totalNbTasksData?.total_nb_tasks;
  console.log("totalNbTasksData", totalNbTasksData);

  const { data: mostDetectedEventData } = useSWR(
    [
      `/api/explore/${project_id}/aggregated/tasks`,
      accessToken,
      flagFilter,
      eventFilter,
      "most_detected_event",
    ],
    ([url, accessToken]) =>
      authFetcher(url, accessToken, "POST", {
        metrics: ["most_detected_event"],
        tasks_filter: {
          flag: flagFilter,
          event_name: eventFilter,
        },
      }),
  );
  const mostDetectedEvent: string | null | undefined =
    mostDetectedEventData?.most_detected_event;
  console.log("mostDetectedEventData", mostDetectedEventData);

  const { data: globalSuccessRateData } = useSWR(
    [
      `/api/explore/${project_id}/aggregated/tasks`,
      accessToken,
      flagFilter,
      eventFilter,
      "global_success_rate",
    ],
    ([url, accessToken]) =>
      authFetcher(url, accessToken, "POST", {
        metrics: ["global_success_rate"],
        tasks_filter: {
          flag: flagFilter,
          event_name: eventFilter,
        },
      }),
  );
  const globalSuccessRate: number | null | undefined = Math.round(
    (globalSuccessRateData?.global_success_rate * 10000) / 100,
  );

  const { data: nbDailyTasks }: { data: NbDailyTasks[] | null | undefined } =
    useSWR(
      [
        `/api/explore/${project_id}/aggregated/tasks`,
        accessToken,
        flagFilter,
        eventFilter,
        "nb_daily_tasks",
      ],
      ([url, accessToken]) =>
        authFetcher(url, accessToken, "POST", {
          metrics: ["nb_daily_tasks"],
          tasks_filter: {
            flag: flagFilter,
            event_name: eventFilter,
          },
        }).then((data) => {
          return data?.nb_daily_tasks?.map((nb_daily_task: NbDailyTasks) => {
            const date = new Date(nb_daily_task.date);
            nb_daily_task.day = date.toLocaleDateString("en-US", {
              weekday: "short",
            });
            return nb_daily_task;
          });
        }),
    );

  const { data: eventsRanking }: { data: EventsRanking[] | null | undefined } =
    useSWR(
      [
        `/api/explore/${project_id}/aggregated/tasks`,
        accessToken,
        flagFilter,
        eventFilter,
        "events_ranking",
      ],
      ([url, accessToken]) =>
        authFetcher(url, accessToken, "POST", {
          metrics: ["events_ranking"],
          tasks_filter: {
            flag: flagFilter,
            event_name: eventFilter,
          },
        }).then((data) =>
          data?.events_ranking?.sort(
            (a: EventsRanking, b: EventsRanking) => b.nb_events - a.nb_events,
          ),
        ),
    );

  const {
    data: successRatePerTaskPosition,
  }: {
    data: SuccessRateByPosition[] | null | undefined;
  } = useSWR(
    [
      `/api/explore/${project_id}/aggregated/tasks`,
      accessToken,
      flagFilter,
      eventFilter,
      "success_rate_per_task_position",
    ],
    ([url, accessToken]) =>
      authFetcher(url, accessToken, "POST", {
        metrics: ["success_rate_per_task_position"],
        tasks_filter: {
          flag: flagFilter,
          event_name: eventFilter,
        },
      }).then((data) => {
        return data?.success_rate_per_task_position?.map(
          (success_rate: SuccessRateByPosition) => {
            success_rate.success_rate =
              Math.round(success_rate.success_rate * 10000) / 100;
            return success_rate;
          },
        );
      }),
  );

  if (!project_id) {
    return <></>;
  }

  return (
    <div>
      <div className="container mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <Card>
              <CardHeader>
                <CardDescription>Total Nb of Tasks</CardDescription>
              </CardHeader>
              <CardContent>
                {((totalNbTasks === null || totalNbTasks === undefined) && (
                  <p>...</p>
                )) || <p className="text-xl">{totalNbTasks}</p>}
              </CardContent>
            </Card>
          </div>
          <div className="ml-4 mr-4">
            <Card className="overflow-hidden">
              <CardHeader>
                <CardDescription>Most Detected Event</CardDescription>
              </CardHeader>
              <CardContent>
                {(!mostDetectedEvent && <p>...</p>) || (
                  <p className="text-xl">{mostDetectedEvent}</p>
                )}
              </CardContent>
            </Card>
          </div>
          <div>
            <Card>
              <CardHeader>
                <CardDescription>Average Task Success Rate</CardDescription>
              </CardHeader>
              <CardContent>
                {((globalSuccessRate === null ||
                  globalSuccessRate === undefined) && <p>...</p>) || (
                  <p className="text-xl">{globalSuccessRate} %</p>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
      <div className="container mx-auto mt-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex-1">
            <h3 className="text-slate-500 mb-2">Nb of tasks per day</h3>
            {(!nbDailyTasks && <Skeleton className="w-[100%] h-[150px]" />) ||
              (nbDailyTasks && (
                <ResponsiveContainer width="100%" height={150}>
                  <BarChart
                    width={300}
                    height={250}
                    data={nbDailyTasks}
                    barGap={0}
                    barCategoryGap={0}
                  >
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Bar
                      dataKey="nb_tasks"
                      fill="#22c55e"
                      radius={[4, 4, 0, 0]}
                      barSize={20}
                    />
                  </BarChart>
                </ResponsiveContainer>
              ))}
          </div>
          <div className="flex-1">
            <h3 className="text-slate-500 mb-2">Top events (last 7d)</h3>
            {(!eventsRanking && <Skeleton className="w-[100%] h-[150px]" />) ||
              (eventsRanking && (
                <ResponsiveContainer className="flex justify-end" height={150}>
                  <BarChart
                    // width={300}
                    height={250}
                    data={eventsRanking}
                    barGap={0}
                    barCategoryGap={0}
                    layout="horizontal"
                  >
                    <YAxis type="number" />
                    <XAxis
                      dataKey="event_name"
                      type="category"
                      fontSize={12}
                      overflow={"visible"}
                      // angle={-45} // Rotate the labels by 45 degrees
                    />
                    <Tooltip />
                    <Bar
                      dataKey="nb_events"
                      fill="#22c55e"
                      radius={[0, 4, 4, 0]}
                      barSize={20}
                    />
                  </BarChart>
                </ResponsiveContainer>
              ))}
          </div>
          <div className="flex-1">
            <h3 className="text-slate-500 mb-2">
              Success Rate per task position
            </h3>
            {hasSessions && !successRatePerTaskPosition && (
              <Skeleton className="w-[100%] h-[150px]" />
            )}
            {!hasSessions && !successRatePerTaskPosition && (
              // Add a button in the center with a CTA "setup session tracking"
              <div className="flex flex-col text-center items-center h-full">
                <p className="text-gray-500 mb-4">
                  This metric is only available
                  <br /> with session tracking
                </p>
                <Link
                  href="https://docs.phospho.ai/guides/sessions-and-users#sessions"
                  target="_blank"
                >
                  <Button variant="outline">Setup session tracking</Button>
                </Link>
              </div>
            )}
            {successRatePerTaskPosition && (
              <ResponsiveContainer width="100%" height={150}>
                <AreaChart
                  width={730}
                  height={250}
                  data={successRatePerTaskPosition}
                  // margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                >
                  <defs>
                    <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#22c55e" stopOpacity={0.8} />
                      <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="task_position" className="text-slate-500" />
                  <YAxis unit="%" />
                  <Tooltip />
                  <Area
                    type="monotone"
                    dataKey="success_rate"
                    stroke="#22c55e"
                    fillOpacity={1}
                    fill="url(#colorUv)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TasksDataviz;
