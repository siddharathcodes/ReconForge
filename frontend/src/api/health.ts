import { apiClient } from './client'

export type HealthCheck = {
  status: 'ok'
  service: string
  version: string
  checks: Record<string, string>
}

export async function getHealth(): Promise<HealthCheck> {
  const response = await apiClient.get<HealthCheck>('/health')
  return response.data
}
