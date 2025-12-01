import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  try {
    const transactions = await prisma.transaction.findMany({
      include: {
        product: {
          include: {
            category: true,
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    });
    return NextResponse.json(transactions);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch transactions' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { productId, type, quantity, reason, notes } = body;

    // Create transaction
    const transaction = await prisma.transaction.create({
      data: {
        productId,
        type,
        quantity,
        reason,
        notes,
      },
      include: {
        product: {
          include: {
            category: true,
          },
        },
      },
    });

    // Update inventory
    const inventory = await prisma.inventory.findUnique({
      where: { productId },
    });

    if (inventory) {
      const newQuantity = type === 'ENTRY' 
        ? inventory.quantity + quantity 
        : inventory.quantity - quantity;

      await prisma.inventory.update({
        where: { productId },
        data: { quantity: Math.max(0, newQuantity) },
      });
    }

    return NextResponse.json(transaction, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create transaction' },
      { status: 500 }
    );
  }
}
