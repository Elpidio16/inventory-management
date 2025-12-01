import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  try {
    const products = await prisma.product.findMany({
      include: {
        category: true,
        inventory: true,
      },
    });
    return NextResponse.json(products);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch products' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { name, description, sku, price, categoryId } = body;

    const product = await prisma.product.create({
      data: {
        name,
        description,
        sku,
        price: parseFloat(price),
        categoryId,
        inventory: {
          create: {
            quantity: 0,
          },
        },
      },
      include: {
        category: true,
        inventory: true,
      },
    });

    return NextResponse.json(product, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create product' },
      { status: 500 }
    );
  }
}
