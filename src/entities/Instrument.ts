import { Entity, PrimaryColumn, Column } from "typeorm";

@Entity()
export class Instrument {
    @PrimaryColumn()
    id: string;

    @Column()
    symbol: string;

    @Column({ nullable: true })
    isin: string;

    @Column()
    name: string;

    @Column({ type: 'json', nullable: true })
    additionalData: Record<string, any>;

    @Column()
    lastUpdated: Date;
}
