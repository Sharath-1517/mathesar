<script lang="ts">
  import { _ } from 'svelte-i18n';

  import type { Tab } from '@mathesar/component-library/types';
  import { TabContainer, defined } from '@mathesar-component-library';

  import CellMode from './cell/CellMode.svelte';
  import ColumnMode from './column/ColumnMode.svelte';
  import RecordMode from './record/RecordMode.svelte';
  import TableMode from './table/TableMode.svelte';

  const tabMap = {
    table: { label: $_('table'), component: TableMode },
    column: { label: $_('column'), component: ColumnMode },
    record: { label: $_('record'), component: RecordMode },
    cell: { label: $_('cell'), component: CellMode },
  };

  type TableInspectorTabId = keyof typeof tabMap;

  export let activeTabId: TableInspectorTabId | undefined;

  $: tabs = Object.entries(tabMap).map(([id, tab]) => ({ id, ...tab }));
  $: activeTab = defined(activeTabId, (id) => ({ id, ...tabMap[id] }));

  function handleTabSelected(e: CustomEvent<{ tab: Tab }>) {
    activeTabId = e.detail.tab.id as TableInspectorTabId;
  }
</script>

<div class="table-inspector">
  <TabContainer
    {activeTab}
    {tabs}
    tabStyle="compact"
    fillContainerHeight
    fillTabWidth
    on:tabSelected={handleTabSelected}
  >
    {#if activeTab}
      <div class="tabs-container">
        <svelte:component this={activeTab.component} />
      </div>
    {/if}
  </TabContainer>
</div>

<style lang="scss">
  .table-inspector {
    height: 100%;
    box-shadow:
      0 10px 15px -3px rgba(0, 0, 0, 0.1),
      0 4px 6px -2px rgba(0, 0, 0, 0.05);
    position: relative;
    background-color: var(--sand-100);
    border-left: solid var(--slate-300) 1px;
    isolation: isolate;

    .tabs-container {
      padding: var(--size-super-ultra-small);
    }
  }
</style>
