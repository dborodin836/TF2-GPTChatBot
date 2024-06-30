import React, { useEffect, useState } from 'react';
import { Card, Typography } from '@material-tailwind/react';
import { pieArcLabelClasses, PieChart } from '@mui/x-charts';
import { useAlert } from '../AlertContext';

export function Dashboard() {
  const [statsData, setStatsData] = useState<any>([]);
  const { openAlert } = useAlert();

  const fetchLineStats = async () => {
    const response = await fetch(`http://127.0.0.1:8000/stats/`);
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
      console.log(resultArray);
      setStatsData(resultArray);
    }
  };

  useEffect(() => {
    fetchLineStats();

    // Set up the interval to fetch data periodically
    const interval = setInterval(() => {
      fetchLineStats();
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
      <div className="p-4 bg-green-500 text-white h-full">Item 2</div>
      <div className="p-4 bg-red-500 text-white h-full">Item 3</div>
      <div className="p-4 bg-yellow-500 text-white h-full">Item 4</div>
    </div>

  );
}
