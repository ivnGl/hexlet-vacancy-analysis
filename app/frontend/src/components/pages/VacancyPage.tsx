import { router } from '@inertiajs/react';
import { Flex, Pagination, TextInput } from '@mantine/core';
import type { ChangeEvent } from 'react';
import { useCallback, useEffect, useMemo, useState } from 'react';

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

function VacancyPage({ vacancies, pagination }: VacancyPageProps) {
  const [query, setQuery] = useState<QueryState>(DEFAULT_QUERY);
console.log(vacancies)
  const handlePageChange = useCallback(
    (pageNumber: number) => {
      router.get('', { ...query, page: pageNumber }, { preserveState: true, replace: true });
    },
    [query],
  );

  const handleSearch = useCallback((event: ChangeEvent<HTMLInputElement>) => {
    setQuery((prev) => ({ ...prev, search: event.target.value }));
  }, []);

  const hasVacancies = useMemo(() => vacancies && vacancies.length > 0, [vacancies]);

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
        placeholder="Search vacancies"
        rightSectionWidth={42}
        onChange={handleSearch}
        value={query.search}
      />

      {hasVacancies && (
        <Flex direction="column" gap="md">
          {vacancies.map((vacancy) => (
            <VacancyCard key={vacancy.id} props={vacancy} />
          ))}
        </Flex>
      )}

      <Pagination
        total={pagination.total_pages}
        value={pagination.current_page}
        onChange={handlePageChange}
        mt="sm"
      />
    </>
  );
}

export default VacancyPage;