import React, { useEffect, useState } from 'react';
import { Card, Typography } from '@material-tailwind/react';
import { Gauge, gaugeClasses, pieArcLabelClasses, PieChart } from '@mui/x-charts';
import { useAlert } from '../AlertContext';

export function Dashboard() {
  const [statsData, setStatsData] = useState<any>([]);
  const [CPMData, setCPMData] = useState<number>(0);
  const [activeUsers, setActiveUsers] = useState<Array<any>>([]);
  const [popularCommands, setPopularCommands] = useState<Array<any>>([]);
  const { openAlert } = useAlert();

  const fetchStats = async () => {
    const response = await fetch(`http://127.0.0.1:8000/stats`);
    if (!response.ok) {
      console.error('Failed to fetch command data');
      openAlert('Failed to fetch command data.');
    } else {
      let data = await response.json();
      data = JSON.parse(data);
      let resultArray = [
        { id: 0, value: data.chat_messages_parsed_count, label: 'Chat' },
        { id: 1, value: data.stats_commands_parsed_count, label: 'Stats' },
        {
          id: 2,
          value: data.total_lines_parsed_count - (data.chat_messages_parsed_count + data.stats_commands_parsed_count),
          label: 'System',
        },
      ];
      console.log(data);
      setPopularCommands(data.most_used_commands);
      setActiveUsers(data.most_active_users);
      setCPMData(data.request_per_minute);
      setStatsData(resultArray);
    }
  };

  useEffect(() => {
    fetchStats();

    // Set up the interval to fetch data periodically
    const interval = setInterval(() => {
      fetchStats();
    }, 2000);  // 2s

    // Clean up the interval on component unmount
    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="grid grid-cols-2 grid-rows-2 gap-4 px-4 pt-4 pb-8 bg-white h-screen">
      <Card className="p-4 h-full">
        <Typography>Parsed Lines</Typography>
        <PieChart
          colors={['#6dd56b', '#7692FF', '#D66BA0']}
          series={[
            {
              data: statsData,
              cornerRadius: 5,
              paddingAngle: 1,
              arcLabel: (item) => `${item.value}`,
              arcLabelMinAngle: 25,
              highlightScope: { faded: 'global', highlighted: 'item' },
              faded: { color: 'gray' },
            },
          ]}
          sx={{
            [`& .${pieArcLabelClasses.root}`]: {
              fill: 'white',
              fontWeight: 'bold',
            },
          }}
        />
      </Card>
      <Card className="p-4 h-full">
        <Typography>Request per minute</Typography>
        <Gauge
          cornerRadius="50%"
          value={CPMData}
          startAngle={-110}
          endAngle={110}
          valueMax={40}
          sx={(theme) => ({
            [`& .${gaugeClasses.valueText}`]: {
              fontSize: 40,
            },
            [`& .${gaugeClasses.valueArc}`]: {
              fill: '#52b202',
            },
            [`& .${gaugeClasses.referenceArc}`]: {
              fill: theme.palette.text.disabled,
            },
          })}
        />
      </Card>
      <Card className="p-4 h-full">
        <Typography>Most active users</Typography>
        <ol className="mt-2 flex flex-col h-full">
          {activeUsers.map((user, index) => (
            <li key={index} className="text-xl pb-2 flex justify-between">
              <span>{index + 1}. {user.username}</span>
              <span>{user.calls} request(s)</span>
            </li>
          ))}
        </ol>
      </Card>
      <Card className="p-4 h-full">
        <Typography>Popular commands</Typography>
        <ol className="mt-2 flex flex-col h-full">
          {popularCommands.map((user, index) => (
            <li key={index} className="text-xl pb-2 flex justify-between">
              <span>{index + 1}. {user.name}</span>
              <span>{user.calls} request(s)</span>
            </li>
          ))}
        </ol>
      </Card>
    </div>

  );
}
