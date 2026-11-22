export type Role = "user" | "agent" | "admin";
export type Status = "open" | "in_progress" | "resolved" | "closed";
export type Priority = "low" | "normal" | "high" | "critical";
export type Category = "hardware" | "software" | "network" | "access" | "other";

export interface UserBrief { id: number; full_name: string; email: string; role: Role }
export interface User extends UserBrief { is_active: boolean; created_at: string; last_login_at: string | null }

export interface Ticket {
  id: number;
  title: string;
  description: string;
  status: Status;
  priority: Priority;
  category: Category;
  requester: UserBrief;
  assignee: UserBrief | null;
  created_at: string;
  updated_at: string;
  resolved_at: string | null;
  closed_at: string | null;
  comment_count: number;
}

export interface Comment { id: number; body: string; author: UserBrief; created_at: string }
export interface TicketEvent {
  id: number;
  kind: string;
  from_value: string | null;
  to_value: string | null;
  actor: UserBrief;
  created_at: string;
}
export interface TicketDetail extends Ticket {
  comments: Comment[];
  events: TicketEvent[];
  allowed_transitions: Status[];
  can_edit: boolean;
}
export interface TicketPage { items: Ticket[]; total: number; page: number; page_size: number; pages: number }

export interface Stats {
  total: number;
  by_status: Record<Status, number>;
  by_priority: Record<Priority, number>;
  by_category: Record<Category, number>;
  unassigned_open: number;
  assigned_to_me: number;
  mine_active: number;
  critical_open: number;
  avg_resolution_hours: number | null;
  timeline: { date: string; created: number; resolved: number }[];
  agents: { id: number; full_name: string; open: number }[];
}

export interface TokenResponse { access_token: string; expires_in: number; user: User }

export interface BrowserSessionResponse { expires_in: number; user: User }
