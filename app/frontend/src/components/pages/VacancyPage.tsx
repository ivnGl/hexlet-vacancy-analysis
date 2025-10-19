import { Flex, Group, Paper, Text } from '@mantine/core';


function VacancyCard({ vacancy }) {
  return (
    <>
      <Paper shadow='lg' withBorder radius='lg'>
        <h3>{vacancy.title}</h3>
        <Group variant='red' justify='space-around'>
          <h4>{vacancy.company}</h4>
          <Text>город {vacancy.city}</Text>
        </Group>


        <Group>
          <Text>оплата {vacancy.salary}</Text>
      </Group>


      </Paper>
    </>
  )
}
function VacancyPage({vacancies}) {

    return (
      <>
         <Flex direction='column' gap="md">
          {vacancies.map(vacancy => <VacancyCard vacancy={vacancy} />)}
          </Flex>
        </>
  );
}


export default VacancyPage