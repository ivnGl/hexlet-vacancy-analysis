import { router } from '@inertiajs/react';
import { Box, Container, Pagination, TextInput } from '@mantine/core';
import type { ChangeEvent } from 'react';
import { useCallback, useEffect, useState } from 'react';

import { useDebounce } from '../../hooks/useDebounce';
import type { VacancyCardProps } from '../../types';
import { VacancyCard } from '../shared/VacancyCard';

type PaginationMeta = {
  total_pages: number;
  current_page: number;
};

type VacancyPageProps = {
  vacancies: VacancyCardProps[];
  pagination: PaginationMeta;
};

type QueryState = {
  search: string;
};

const DEFAULT_QUERY: QueryState = { search: '' };
const QUERY_DELAY: number = 2000


function VacancyPage({ vacancies, pagination }: VacancyPageProps) {
  const [query, setQuery] = useState<QueryState>(DEFAULT_QUERY);
  const debouncedQuery = useDebounce(query, QUERY_DELAY)

  const handlePageChange = useCallback(
    (pageNumber: number) => {
      router.get('', { ...debouncedQuery, page: pageNumber }, { preserveState: true, replace: true });
    },
    [debouncedQuery],
  );

  const handleSearch = (event: ChangeEvent<HTMLInputElement>) => {
    setQuery((prev) => ({ ...prev, search: event.target.value }));
  };

  useEffect(() => {
    router.get('', { ...debouncedQuery, page: 1 }, {
      preserveState: true,
      replace: true,
    });
  }, [debouncedQuery]);

  if (!vacancies) return "Loading..."

  return (
    <Container>
      <Box mb={20} mt="xs">
        <TextInput
          radius="xl"
          size="md"
          placeholder="Search vacancies"
          rightSectionWidth={42}
          onChange={handleSearch}
          value={query.search}
        />
      </Box>

      {vacancies.map((vacancy) => (
        <VacancyCard key={vacancy.id} props={vacancy} />
      ))}

      <Pagination
        total={pagination.total_pages}
        value={pagination.current_page}
        onChange={handlePageChange}
        mt="sm"
      />

    </Container>
  );
}

export default VacancyPage;