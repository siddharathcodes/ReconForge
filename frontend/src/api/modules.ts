import { apiClient } from './client'

export type ModuleStatus = 'foundation' | 'planned' | 'active'

export type ReconModule = {
  key: string
  name: string
  description: string
  status: ModuleStatus
  route: string
  worker_queues: string[]
}

type ModuleCatalogResponse = {
  modules: ReconModule[]
}

export async function getModules(): Promise<ReconModule[]> {
  const response = await apiClient.get<ModuleCatalogResponse>('/modules')
  return response.data.modules
}
