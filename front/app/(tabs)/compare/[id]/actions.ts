"use server";

import { fetchBackend, type Product } from "@/lib/backend-api";

export default async function fetchProductDetails(id: string): Promise<Product> {
  const productId = decodeURIComponent(id);
  return fetchBackend<Product>(`/api/products/${encodeURIComponent(productId)}`);
}
