import { router } from '@inertiajs/react';
import { Flex, Group, Pagination, Paper, Text, TextInput } from '@mantine/core';
import { useEffect, useState } from 'react';


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
function VacancyPage({ vacancies, pagination }) {

  const [query, setQuery] = useState({
    search: ""
  });

  function handlePageChange(pageNumber: number) {
    router.get(`?page=${pageNumber}`)

  }

  function handleSearch(e) {
    const search = e.target.value
    setQuery({ ...query, search })
  }

  useEffect(() => {
    router.get('', query, {
      preserveState: true,
      replace: true,
    });
  }, [query]);

  return (
    <>
      <TextInput
        radius="xl"
        size="md"
        placeholder="Search questions"
        rightSectionWidth={42}
        onChange={handleSearch}
        value={query.search}
      />
      <Flex direction='column' gap="md">
        {vacancies.map(vacancy => <VacancyCard vacancy={vacancy} />)}
      </Flex>

      <Pagination total={pagination.total_pages} value={pagination.current_page} onChange={handlePageChange} mt="sm" />
    </>
  );
}


export default VacancyPage